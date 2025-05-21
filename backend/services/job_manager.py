from typing import Dict, Optional
import time
from services.logger import job_logger

class JobManager:
    def __init__(self):
        self.jobs: Dict[str, dict] = {}
        job_logger.info("Initialized JobManager")
    
    def update_job(self, job_id: str, status: str, result_path: Optional[str] = None, error: Optional[str] = None):
        """Update the status and result of a job."""
        job_logger.info(f"Updating job {job_id} - Status: {status}")
        
        self.jobs[job_id] = {
            "status": status,
            "result_path": result_path,
            "error": error,
            "updated_at": time.time()
        }
        
        if error:
            job_logger.error(f"Job {job_id} failed: {error}")
        elif status == "completed":
            job_logger.info(f"Job {job_id} completed successfully")
    
    def get_job(self, job_id: str) -> Optional[dict]:
        """Get the current status and result of a job."""
        job = self.jobs.get(job_id)
        if job:
            job_logger.debug(f"Retrieved job {job_id} - Status: {job['status']}")
        else:
            job_logger.warning(f"Job not found: {job_id}")
        return job
    
    def cleanup_old_jobs(self, max_age_hours: int = 24):
        """Clean up jobs older than max_age_hours."""
        current_time = time.time()
        jobs_to_remove = []
        
        for job_id, job in self.jobs.items():
            if current_time - job["updated_at"] > max_age_hours * 3600:
                jobs_to_remove.append(job_id)
        
        if jobs_to_remove:
            job_logger.info(f"Cleaning up {len(jobs_to_remove)} old jobs")
            for job_id in jobs_to_remove:
                del self.jobs[job_id]
                job_logger.debug(f"Removed old job: {job_id}") 