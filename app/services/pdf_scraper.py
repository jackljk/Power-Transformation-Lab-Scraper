import json
import os
import logging
from typing import Dict, Any, Optional, List, Union

import pymupdf4llm
from langchain_openai import ChatOpenAI
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA

from app.models.tasks_models import Task
from app.models.llm_models import get_llm_instance

logger = logging.getLogger(__name__)

class PDFScraper:
    """
    This class is responsible for extracting information from PDF files using LLMs.
    It converts PDFs to markdown, chunks the content, and uses retrieval-augmented generation
    to answer queries about the documents.
    
    Supports processing of single or multiple PDF files.
    """

    def __init__(
        self,
        pdf_paths: Union[str, List[str]],
        prompt: str,
        task_template: str = "default_pdf",
        additional_context: Optional[Dict[str, Any]] = None,
        output_format: Optional[Dict[str, Any]] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """
        Initialize the PDFScraper.
        
        Args:
            pdf_paths: Path to a single PDF file or list of paths to multiple PDF files
            prompt: The prompt or query to extract information from the PDFs
            task_template: The template name for the task
            additional_context: Optional additional context to help with extraction
            output_format: The format of the output data
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between text chunks
        """
        assert pdf_paths, "PDF file path(s) are required"
        assert prompt, "Prompt is required"
        # Convert single path to list for consistent handling
        if isinstance(pdf_paths, str):
            pdf_paths = [pdf_paths]
            
        # Validate that all PDF files exist
        for pdf_path in pdf_paths:
            assert pdf_path and os.path.exists(pdf_path), f"PDF file not found at {pdf_path}"
        
        # Convert additional_context to string format if provided
        additional_context_str = (
            str(additional_context) if additional_context else "None provided"
        )
        
        # Create a Task instance from the specified template
        task_string = Task.from_template(
            template_name=task_template,
            prompt=prompt,
        ).get_task_string()
        
        # Store task-related properties
        self.task_string = task_string
        self.additional_context = additional_context_str
        self.pdf_paths = pdf_paths
        self.prompt = prompt
        self.task_template = task_template
        self.output_format = output_format
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Get the LLM instance
        self.llm = get_llm_instance()
        
        # Initialize QA chain
        self._init_qa_chain()
        
        # Initialize content for query
        self._init_content()
        
    async def scrape(self) -> Dict[str, Any]:
        """
        Scrape information from the PDF based on the prompt.
        
        Returns:
            A dictionary with the extracted information
        """
        try:
            # Execute the query against the PDF content
            response = self.qa_chain.invoke(self.content)
            
            # Log the response if log_response hook is available
            try:
                from app.services.hooks.pdf_scraper_hooks import log_response
                log_response(response)
            except ImportError:
                logger.info("PDF scraper hooks not available, skipping response logging")
            
            # Parse the JSON response if output_format was specified
            if self.output_format:
                try:
                    # Handle case where response might be wrapped in markdown code blocks
                    cleaned_response = response.replace("```json", "").replace("```", "").strip()
                    # Parse the JSON response
                    results = json.loads(cleaned_response)
                    return results
                except json.JSONDecodeError:
                    # If parsing fails, use LLM to convert to proper JSON
                    logger.warning("Failed to parse JSON response, attempting to fix with LLM")
                    fixed_json = self._fix_json_with_llm(cleaned_response)
                    return fixed_json
                except AttributeError:
                    # Handle case where response is already a dictionary
                    if isinstance(response, dict):
                        return response
                    else:
                        logger.error("Unexpected response format, unable to parse. Returning raw response.")
                        logger.error(f"Response content: {response}")
                        return {"error": "Unexpected response format", "content": response}
            # Return the raw response if no output format was specified
            return {"content": response}
            
        except Exception as e:
            logger.error(f"Error during PDF scraping: {str(e)}")
            return {"error": str(e)}
        

    def _init_qa_chain(self):
        """
        Initialize the Question-Answering chain by:
        1. Converting PDFs to markdown
        2. Chunking the text
        3. Creating vector embeddings
        4. Setting up the retrieval system
        
        Processes all PDFs and combines them into a single vector store.
        """
        try:
            all_documents = []
            
            # Create text splitter
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size, 
                chunk_overlap=self.chunk_overlap
            )
            
            logger.info(f"Initializing QA chain for {len(self.pdf_paths)} PDFs")
            # Process each PDF file
            for pdf_path in self.pdf_paths:
                try:
                    # Convert PDF to markdown
                    markdown_text = pymupdf4llm.to_markdown(pdf_path)
                    
                    # Split text into documents with source metadata
                    documents = splitter.create_documents(
                        [markdown_text],
                        metadatas=[{"source": pdf_path}]
                    )
                    
                    # Add to combined document list
                    all_documents.extend(documents)
                    
                    logger.info(f"Successfully processed PDF: {pdf_path}")
                    
                except Exception as e:
                    logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
                    # Continue with other PDFs even if one fails
            
            # Make sure we have at least some documents to process
            if not all_documents:
                raise ValueError("No PDF documents were successfully processed")
            
            logger.info(f"Total documents created from PDFs: {len(all_documents)}")
            logger.debug("Creating vector store from documents")
            # Create vector store from all documents
            vectorstore = FAISS.from_documents(
                all_documents, 
                OpenAIEmbeddings()
            )
            
            # Set up retriever
            retriever = vectorstore.as_retriever()
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=retriever
            )
            
            logger.info(f"Successfully initialized QA chain for {len(self.pdf_paths)} PDFs")
            
        except Exception as e:
            logger.error(f"Failed to initialize QA chain: {str(e)}")
            raise    
    def _init_content(self):
        """
        Initialize the content string for scraping.
        - Combines the prompt, additional context, and output format.
        """
        # Format the output formatting instructions
        output_format_str = (
            json.dumps(self.output_format, indent=2) 
            if self.output_format 
            else "Provide a detailed response."
        )
        
        # Format the list of PDF files
        pdf_files_str = "\n        ".join(self.pdf_paths)
        
        self.content = f"""
        PDF file(s): 
        {pdf_files_str}
        
        Task: {self.task_string}
        Prompt: {self.prompt}
        Additional context: {self.additional_context}
        
        Please extract the requested information from the PDF document(s) and format your response according to the following structure:
        {output_format_str}
        """


    def _fix_json_with_llm(self, response_text: str) -> Dict[str, Any]:
        """
        Use the LLM to fix malformed JSON responses.
        
        Args:
            response_text: The malformed JSON text
            
        Returns:
            Properly formatted JSON as a dictionary
        """
        try:
            # Create a prompt to fix the JSON
            fix_prompt = f"""
            The following text should be valid JSON but may have formatting issues.
            Please convert it to proper, valid JSON format:
            
            {response_text}
            
            Return ONLY the corrected JSON with no additional text or explanation.
            """
            
            # Use the LLM to fix the JSON
            corrected = self.llm.invoke(fix_prompt).content
            
            # Remove any markdown formatting or explanations
            corrected = corrected.replace("```json", "").replace("```", "").strip()
            
            # Parse the corrected JSON
            return json.loads(corrected)
            
        except Exception as e:
            logger.error(f"Failed to fix JSON with LLM: {str(e)}")
            # Return the original response as plain text if fixing fails
            return {"content": response_text, "parsing_error": str(e)}

    def extract_specific_info(self, specific_query: str) -> Dict[str, Any]:
        """
        Extract specific information from the PDF based on a new query.
        Useful for follow-up questions after the initial scraping.
        
        Args:
            specific_query: The specific question to ask about the PDF
            
        Returns:
            The response as a dictionary
        """
        try:
            # Execute the specific query against the PDF content
            response = self.qa_chain.run(specific_query)
            
            # If the response is expected to be JSON, attempt to parse it
            try:
                # Clean up potential markdown formatting
                cleaned_response = response.replace("```json", "").replace("```", "").strip()
                results = json.loads(cleaned_response)
                return results
            except json.JSONDecodeError:
                # Return as plain text if not valid JSON
                return {"content": response}
                
        except Exception as e:
            logger.error(f"Error during specific info extraction: {str(e)}")
            return {"error": str(e)}