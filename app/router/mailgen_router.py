from fastapi import APIRouter, Depends, HTTPException,status, Header, BackgroundTasks,Security, UploadFile, File, Form, Query, Body, Request
# from sse_starlette.sse import EventSourceResponse
# from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from pydantic import HttpUrl
from urllib.parse import urljoin
import requests
from typing import List, Dict, Union, Optional
from datetime import datetime
import io
import os
import httpx
from typing import Optional
from app.utilities.mail_verify_utils import verify_emails
from fastapi.responses import StreamingResponse
from app.schemas.meta_schemas import EmailLookupRequest, MetaDataResponse
from app.utilities.meta_utils import extract_facebook_pages
from app.utilities.facebookpage_scrap import scrape_facebook_page_about,scrape_facebook_page_transparency
router = APIRouter()

# ------------------------------
# API Endpoints
# ------------------------------

@router.post("/verify-emails/")
async def verify_email_list(
    file: Optional[UploadFile] = File(None),
    emails: Optional[List[str]] = Form(None)
):
    """
    Verify emails provided either as:
    - A file upload (one email per line)
    - A form field containing a JSON list of emails
    """
    print(emails, "emails")
    try:
        input_emails = []

        # If file is provided
        if file:
            contents = await file.read()
            decoded = contents.decode("utf-8")
            input_emails = [line.strip() for line in io.StringIO(decoded) if line.strip()]

        # If emails are provided in form
        if emails:
            input_emails.extend(emails)

        if not input_emails:
            return JSONResponse(content={"error": "No emails provided."}, status_code=400)

        valid_emails = verify_emails(list(set(input_emails)))  # Remove duplicates
        return {
            "total_emails_received": len(input_emails),
            "valid_emails_count": len(valid_emails),
            "valid_emails": valid_emails
        }

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



# response_model=MetaDataResponse
@router.post("/meta/enrich")
async def enrich_via_meta(request: EmailLookupRequest):
    """
    Given a business email, find the linked Facebook/Instagram data
    """
    domain_part = request.email.split('@')[1]  # 'etrade.com'
    # Split the domain by '.' and take the first part
    domain_name = domain_part.split('.')[0]  # 'etrade'
    pages = extract_facebook_pages(domain_name)

    for page_link in pages:
        print("about", f"{page_link}about")
        about=scrape_facebook_page_about(f"{page_link}about")
        # Safely get transparency_page
        transparency_page_link = about.get('websites', {}).get('transparency_page')
        print("about", about)
        page_transparency=scrape_facebook_page_transparency(transparency_page_link)
        print("page_transparency", page_transparency)

    return {"pages": pages}