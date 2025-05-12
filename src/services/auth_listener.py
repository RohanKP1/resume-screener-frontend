import requests
from typing import Dict, Optional
from src.utils.custom_logger import CustomLogger

logger = CustomLogger("AuthListener")

class AuthListener:
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the authentication listener
        
        Args:
            base_url (str): Base URL of the authentication service
        """
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json"
        }
        logger.info(f"AuthListener initialized with base URL: {base_url}")

    def update_token(self, token: str) -> None:
        """
        Update the authorization header with new token
        
        Args:
            token (str): JWT token
        """
        self.headers["Authorization"] = f"Bearer {token}"

    async def register(self, username: str, email: str, password: str, user_type: str) -> Dict:
        """
        Register a new user
        
        Args:
            username (str): Username
            email (str): Email address
            password (str): Password
            user_type (str): Type of user (CANDIDATE/RECRUITER)
            
        Returns:
            Dict: Response from the registration endpoint
        """
        try:
            endpoint = f"{self.base_url}/auth/register"
            payload = {
                "username": username,
                "email": email,
                "password": password,
                "user_type": user_type
            }
            
            logger.info(f"Attempting registration for user: {email}")
            response = requests.post(endpoint, json=payload, headers=self.headers)
            
            if response.status_code == 200:
                logger.info(f"Successfully registered user: {email}")
                return response.json()
            else:
                logger.error(f"Registration failed: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return {"error": str(e)}

    async def login(self, username: str, password: str) -> Dict:
        """
        Login user and get access token
        
        Args:
            username (str): Username or email
            password (str): Password
            
        Returns:
            Dict: Response containing access token if successful
        """
        try:
            endpoint = f"{self.base_url}/auth/token"
            payload = {
                "username": username,
                "password": password
            }
            
            logger.info(f"Attempting login for user: {username}")
            response = requests.post(endpoint, data=payload)
            
            if response.status_code == 200:
                token_data = response.json()
                self.update_token(token_data["access_token"])
                logger.info(f"Successfully logged in user: {username}")
                return token_data
            else:
                logger.error(f"Login failed: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return {"error": str(e)}

    async def update_profile(self, update_data: Dict) -> Dict:
        """
        Update user profile
        
        Args:
            update_data (Dict): Data to update in user profile
            
        Returns:
            Dict: Response from update endpoint
        """
        try:
            endpoint = f"{self.base_url}/auth/users/me"
            
            logger.info("Attempting to update user profile")
            response = requests.put(endpoint, json=update_data, headers=self.headers)
            
            if response.status_code == 200:
                logger.info("Successfully updated user profile")
                return response.json()
            else:
                logger.error(f"Profile update failed: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            logger.error(f"Profile update error: {str(e)}")
            return {"error": str(e)}

    def is_authenticated(self) -> bool:
        """
        Check if user is authenticated
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        return "Authorization" in self.headers