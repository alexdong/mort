import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def extract_urls_from_job_details(job_detail: Dict) -> List[str]:
    return [screenshot['image_url'] for screenshot in job_detail['screenshots']]
