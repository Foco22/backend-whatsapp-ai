import os
import json
import logging
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import PlainTextResponse, JSONResponse
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
TOKEN_VERIFICACION = os.getenv('TOKEN_VERIFICACION')

# Set up logging
logging.basicConfig(level=logging.INFO)
logging.info(f"TOKEN_VERIFICACION: {TOKEN_VERIFICACION}")

@app.get("/webhook")
async def get_webhook(req: Request):
    hub_mode = req.query_params.get('hub.mode')
    hub_challenge = req.query_params.get('hub.challenge')
    hub_verify_token = req.query_params.get('hub.verify_token')
    
    logging.info(f"hub_mode: {hub_mode}, hub_challenge: {hub_challenge}, hub_verify_token: {hub_verify_token}")

    if hub_mode == 'subscribe' and hub_verify_token == TOKEN_VERIFICACION:
        return PlainTextResponse(hub_challenge)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Verification token mismatch")


@app.post("/webhook")
async def post_webhook(request: Request):
    from whatsapp_apis import post_webhook
    try:
        # Add logging to see when the request starts processing
        logging.info("Received a POST request")
        # Read the raw request body
        raw_body = await request.body()
        logging.info(f"Raw request body: {raw_body}")
        # Check if the body is empty
        if not raw_body:
            raise ValueError("Empty request body")
        # Try to parse the JSON body
        body = json.loads(raw_body)
        logging.info(f"Incoming webhook body: {body}")
        post_webhook_instance = post_webhook.PostWebhook(body)
        result = post_webhook_instance.main()
        logging.info(f"Result from PostWebhook: {result}")
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except ValueError as e:
        logging.error(f"ValueError: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid body: {e}")
    except Exception as e:
        logging.error(f"Exception: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
