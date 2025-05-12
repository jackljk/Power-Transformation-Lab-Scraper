import pytest
import yaml
import os
import tempfile
from unittest.mock import patch
from pydantic import ValidationError
from app.models.output_format_models import build_output_model
from typing import Any, get_args


@pytest.fixture
def temp_yaml_config():
    """Create temporary YAML configuration files for testing."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create profiles directory
        profiles_dir = os.path.join(temp_dir, "profiles")
        os.makedirs(profiles_dir)

        # Create a basic test profile
        basic_profile = {
            "name": "basic_profile",
            "content_structure": {
                "Film_Info": {
                    "title": "str",
                    "year": "int",
                    "rating": "float",
                    "is_award_winner": "bool",
                }
            },
        }

        # Create an advanced test profile
        advanced_profile = {
            "name": "advanced_profile",
            "content_structure": {
                "Movie_Details": {
                    "title": "str",
                    "director": "str",
                    "release_year": "int",
                    "box_office": "float",
                    "is_sequel": "bool",
                },
                "Cast_Info": {"actor_name": "str", "role": "str", "is_lead": "bool"},
            },
        }

        # Write the profiles to files
        basic_profile_path = os.path.join(profiles_dir, "test_profile.yaml")
        advanced_profile_path = os.path.join(profiles_dir, "advanced_profile.yaml")

        with open(basic_profile_path, "w", encoding="utf-8") as f:
            yaml.dump(basic_profile, f)

        with open(advanced_profile_path, "w", encoding="utf-8") as f:
            yaml.dump(advanced_profile, f)

        # Return the paths and config data for use in tests
        return {
            "temp_dir": temp_dir,
            "profiles_dir": profiles_dir,
            "basic_profile_path": basic_profile_path,
            "advanced_profile_path": advanced_profile_path,
            "basic_profile": basic_profile,
            "advanced_profile": advanced_profile,
        }


@pytest.mark.parametrize("profile_name", ["basic_profile", "advanced_profile"])
def test_build_scraper_output_model_from_yaml(temp_yaml_config, profile_name):
    """Test building scraper output model from YAML configuration."""
    # Mock the config manager to use our temporary files
    with patch("app.utils.config_manager.config_manager") as mock_config_manager:
        # Set up the mock to return our test data
        profile_data = temp_yaml_config[f"{profile_name}"]
        mock_config_manager.get.return_value = profile_data["content_structure"]

        for content_model_name, fields in profile_data["content_structure"].items():
            # Build the model
            output_model = build_output_model({content_model_name: fields})
            # Verify the model was created correctly
            # First, check the ScraperOutputList model
            assert "outputs" in output_model.__annotations__
            output_list_field = output_model.__annotations__["outputs"]
            
            # Extract the ScraperOutput model from the list field
            scraper_output_model = get_args(output_list_field)[0]
            assert f"{content_model_name}-content" in scraper_output_model.__annotations__
            
            # Extract the content field type (List[ContentModel])
            content_field_type = scraper_output_model.__annotations__[f"{content_model_name}-content"]
            
            # Get the inner content model type
            inner_type = get_args(content_field_type)[0]
            assert inner_type.__name__ == content_model_name

            # Verify the fields in the content model
            model_fields = inner_type.__annotations__
            assert len(model_fields) == len(fields)
            assert all(field in model_fields for field in fields.keys())
            assert all(
                (
                    model_fields[field] is str
                    if fields[field] == "str"
                    else (
                        model_fields[field] is int
                        if fields[field] == "int"
                        else (
                            model_fields[field] is float
                            if fields[field] == "float"
                            else (
                                model_fields[field] is bool
                                if fields[field] == "bool"
                                else False
                            )
                        )
                    )
                )
                for field in fields.keys()
            )

def test_build_scraper_output_model_validation(temp_yaml_config: dict[str, Any]):
    """Test validating data with the built model."""
    # Mock the config manager
    with patch("app.utils.config_manager.config_manager") as mock_config_manager:
        # Use the basic profile for this test and get the content structure
        content_structure = temp_yaml_config["basic_profile"]["content_structure"]
        mock_config_manager.get.return_value = content_structure

        # Build the model
        ScraperOutputList = build_output_model(content_structure)

        # Valid data should create a model instance without errors
        valid_data = {'outputs': [{
            "Film_Info-content": [  # Changed from "Film" to match the content model name
                {
                    "title": "The Godfather",
                    "year": 1972,
                    "rating": 9.2,
                    "is_award_winner": True,
                },
                {
                    "title": "The Dark Knight",
                    "year": 2008,
                    "rating": 9.0,
                    "is_award_winner": True,
                },
            ],
            "format_type": "json",
            "summary": "Two classic films.",
        }]}
        film_info_instance = ScraperOutputList(**valid_data)
        # verify the values in the model instance
        assert film_info_instance.outputs[0].format_type == valid_data["outputs"][0]["format_type"]
        assert film_info_instance.outputs[0].summary == valid_data["outputs"][0]["summary"]

        # Access the content with the correct field name
        # Note: 'Film_Info content' is the field name
        film_info_content = getattr(film_info_instance.outputs[0], "Film_Info-content")
        
        # check the values for content items
        assert film_info_content[0].title == "The Godfather"
        assert film_info_content[0].year == 1972
        assert film_info_content[0].rating == 9.2
        assert film_info_content[0].is_award_winner is True
        
        # Check the second item
        assert film_info_content[1].title == "The Dark Knight"
        assert film_info_content[1].year == 2008

        # Invalid data should raise ValidationError
        invalid_data = {'outputs': [{
            "Film_Info-content": [
                {
                    "title": "Inception",
                    "year": "not an integer",  # Very obviously not an int
                    "rating": "not a float",  # Very obviously not a float
                    "is_award_winner": "not a boolean",  # Very obviously not a bool
                }
            ],
            "format_type": "json",
            "summary": "A mind-bending thriller.",
        }]}
        
        # This should raise a ValidationError because of the invalid types
        with pytest.raises(ValidationError):
            ScraperOutputList(**invalid_data)

# TODO: Mutliple different profile types not implemented yet
# def test_multiple_content_structures(temp_yaml_config: dict[str, Any]):
#     """Test handling multiple content structures in a profile."""
#     # Mock the config manager
#     with patch("app.utils.config_manager.config_manager") as mock_config_manager:
#         # Use the advanced profile for this test and get the content structure
#         content_structure = temp_yaml_config["advanced_profile"]["content_structure"]
#         mock_config_manager.get.return_value = content_structure

#         # Build the model
#         ScraperOutput = build_scraper_output_model(content_structure)

#         # Valid data should create a model instance without errors
#         valid_data = {
#             "content": [
#                 {
#                     "title": "Inception",
#                     "director": "Christopher Nolan",
#                     "release_year": 2010,
#                     "box_office": 829895144.0,
#                     "is_sequel": False,
#                 },
#                 {
#                     "actor_name": "Leonardo DiCaprio",
#                     "role": "Cobb",
#                     "is_lead": True,
#                 },
#             ],
#             "format_type": "json",
#             "summary": "A mind-bending thriller.",
#         }
#         film_info_instance = ScraperOutput(**valid_data)

#         # Verify the values in the model instance
#         assert film_info_instance.format_type == valid_data["format_type"]
#         assert film_info_instance.summary == valid_data["summary"]

#         # Check the type of the content field
#         content_field_type = ScraperOutput.__annotations__["content"]
#         inner_type = get_args(content_field_type)[0]
#         assert inner_type.__name__ == "Movie_Details"
#         assert inner_type.__annotations__["title"] is str
#         assert inner_type.__annotations__["director"] is str
#         assert inner_type.__annotations__["release_year"] is int
#         assert inner_type.__annotations__["box_office"] is float
#         assert inner_type.__annotations__["is_sequel"] is bool

#         assert film_info_instance.content[0].title == "Inception"
#         assert film_info_instance.content[0].director == "Christopher Nolan"
#         assert film_info_instance.content[0].release_year == 2010
#         assert film_info_instance.content[0].box_office == 829895144.0
#         assert film_info_instance.content[0].is_sequel is False

        
#         # Check the type of the second content item
#         second_content_field_type = ScraperOutput.__annotations__["content"].__args__[1]
#         assert second_content_field_type.__name__ == "Cast_Info"
#         assert second_content_field_type.__annotations__["actor_name"] is str
#         assert second_content_field_type.__annotations__["role"] is str
#         assert second_content_field_type.__annotations__["is_lead"] is bool
#         assert film_info_instance.content[1].actor_name == "Leonardo DiCaprio"
#         assert film_info_instance.content[1].role == "Cobb"
#         assert film_info_instance.content[1].is_lead is True
        