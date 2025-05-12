import requests
from typing import Dict, Optional
import os
from src.utils.custom_logger import CustomLogger

logger = CustomLogger("CandidateListener")

class CandidateListener:
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the candidate service listener"""
        self.base_url = base_url
        self.headers = {}
        logger.info("CandidateListener initialized")

    def update_token(self, token: str) -> None:
        """Update authorization header with token"""
        self.headers["Authorization"] = f"Bearer {token}"

    def update_token(self, token: str) -> None:
        """Update authorization header with token"""
        self.headers["Authorization"] = f"Bearer {token}"

    async def upload_resume(self, file_path: str, user_id: str) -> Dict:
        """
        Upload resume file to the server
        """
        try:
            endpoint = f"{self.base_url}/candidate/upload_resume"

            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return {"error": "File not found"}

            # Prepare file for upload
            with open(file_path, 'rb') as file:
                files = {'file': (os.path.basename(file_path), file)}
                data = {'user_id': user_id}

                logger.info(f"Attempting to upload resume for user: {user_id}")
                # Only send Authorization header, not Content-Type
                response = requests.post(
                    endpoint,
                    headers=self.headers,
                    files=files,
                    data=data
                )

            if response.status_code == 200:
                logger.info(f"Successfully uploaded resume for user: {user_id}")
                return response.json()
            else:
                logger.error(f"Resume upload failed: {response.text}")
                return {"error": response.text}

        except Exception as e:
            logger.error(f"Resume upload error: {str(e)}")
            return {"error": str(e)}


    async def get_resume(self, user_id: str) -> Dict:
        """
        Get resume details for a user
        
        Args:
            user_id (str): User ID to fetch resume for
            
        Returns:
            Dict: Resume details
        """
        try:
            endpoint = f"{self.base_url}/candidate/resume"
            
            logger.info(f"Fetching resume for user: {user_id}")
            response = requests.get(endpoint, headers=self.headers)
            
            if response.status_code == 200:
                logger.info(f"Successfully retrieved resume for user: {user_id}")
                return response.json()
            else:
                logger.error(f"Resume retrieval failed: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            logger.error(f"Resume retrieval error: {str(e)}")
            return {"error": str(e)}