import time
import asyncio
import pandas as pd
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from pydantic import BaseModel, ValidationError

from core.utils import combine_serial_numbers
from core.loader import label_decoder, hardware_type_classifier, request_type_classifier
from core.db import add_request, add_serial_number


app = FastAPI()


class RequestData(BaseModel):
    theme: str
    description: str
    

async def generate_answer(theme: str, description: str) -> dict:
    start_time = time.time()
    theme = theme.replace('_x000D_', '')
    description = description.replace('_x000D_', '')

    hardware_type, hardware_type_confidence = hardware_type_classifier.predict(theme, description)
    request_type, request_type_confidence = request_type_classifier.predict(theme, description)

    request_id = await add_request(theme, description, label_decoder.request_type_labels[request_type], 
                                            str(request_type_confidence), label_decoder.hardware_type_labels[hardware_type], 
                                            str(hardware_type_confidence))

    serial_numbers = combine_serial_numbers(theme, description)

    for number in serial_numbers:
        await add_serial_number(request_id, number)


    generation_time = time.time() - start_time
    return {
        "hardware_type": {
            "value": label_decoder.hardware_type_labels[hardware_type],
            "probability": hardware_type_confidence
        },
        "request_type": {
            "value": label_decoder.request_type_labels[request_type],
            "probability": request_type_confidence
        },
        "generation_time": generation_time,
        "serial_numbers": serial_numbers
    }


@app.post("/api/v1/submit_request")
async def submit_request(request: RequestData):
    return await generate_answer(request.theme, request.description)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
