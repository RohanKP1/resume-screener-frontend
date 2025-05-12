import requests
from typing import Dict, Optional
from src.utils.custom_logger import CustomLogger

logger = CustomLogger("JobListener")

class JobListener:
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the job service listener"""
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json"
        }
        logger.info("JobListener initialized")

    def update_token(self, token: str) -> None:
        """Update authorization header with token"""
        self.headers["Authorization"] = f"Bearer {token}"

    async def create_job(self, job_data: Dict) -> Dict:
        """
        Create a new job posting
        
        Args:
            job_data (Dict): Job details including title, description, requirements, etc.
            
        Returns:
            Dict: Created job details
        """
        try:
            endpoint = f"{self.base_url}/job/create_job"
            
            logger.info(f"Creating new job: {job_data.get('title', 'N/A')}")
            response = requests.post(endpoint, json=job_data, headers=self.headers)
            
            if response.status_code == 200:
                logger.info("Job created successfully")
                return response.json()
            else:
                logger.error(f"Job creation failed: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            logger.error(f"Job creation error: {str(e)}")
            return {"error": str(e)}

    async def get_job(self, job_id: str) -> Dict:
        """Get job details by ID"""
        try:
            endpoint = f"{self.base_url}/job/jobs/{job_id}"
            
            logger.info(f"Fetching job details for ID: {job_id}")
            response = requests.get(endpoint, headers=self.headers)
            
            if response.status_code == 200:
                logger.info("Job details retrieved successfully")
                return response.json()
            else:
                logger.error(f"Job retrieval failed: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            logger.error(f"Job retrieval error: {str(e)}")
            return {"error": str(e)}

    async def search_candidates(self, search_params: Dict) -> Dict:
        """Search candidates based on criteria"""
        try:
            endpoint = f"{self.base_url}/candidate/search"
            
            logger.info(f"Searching candidates with params: {search_params}")
            response = requests.get(endpoint, params=search_params, headers=self.headers)
            
            if response.status_code == 200:
                logger.info("Candidate search completed successfully")
                return response.json()
            else:
                logger.error(f"Candidate search failed: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            logger.error(f"Candidate search error: {str(e)}")
            return {"error": str(e)}

    async def rank_candidates(self, job_id: str) -> Dict:
        """Rank candidates for a specific job"""
        try:
            endpoint = f"{self.base_url}/candidate/rank_candidates"
            params = {"job_id": job_id}
            
            logger.info(f"Ranking candidates for job ID: {job_id}")
            response = requests.get(endpoint, params=params, headers=self.headers)
            
            if response.status_code == 200:
                logger.info("Candidates ranked successfully")
                return response.json()
            else:
                logger.error(f"Candidate ranking failed: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            logger.error(f"Candidate ranking error: {str(e)}")
            return {"error": str(e)}

    async def rank_candidates_with_params(self, params: dict) -> dict:
        """Rank candidates for a specific job with extra params"""
        try:
            endpoint = f"{self.base_url}/candidate/rank_candidates"
            logger.info(f"Ranking candidates for job ID: {params.get('job_id')} with params: {params}")
            response = requests.get(endpoint, params=params, headers=self.headers)
            if response.status_code == 200:
                logger.info("Candidates ranked successfully")
                return response.json()
            else:
                logger.error(f"Candidate ranking failed: {response.text}")
                return {"error": response.text}
        except Exception as e:
            logger.error(f"Candidate ranking error: {str(e)}")
            return {"error": str(e)}