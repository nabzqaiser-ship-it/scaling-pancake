import asyncio
import datetime
import json
from operator import itemgetter
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from models import DocumentAnalysis, FileInfo
from llm_config import async_client

app = FastAPI()

files = Path("./data/input")

@app.get("/results/list")
async def list_results():
    output_dir = Path("data/output")

    if not output_dir.exists():
        return { "count": 0, "files": []}
    results = []

    for file in output_dir.glob("*.json"):
        results.append({
            "filename": file.name,
            "size_bytes": file.stat().st_size,
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    results.sort(key=itemgetter('created'), reverse=True)

    return {
        "count:": len(results),
        "files": results
    }

@app.get("/results/{filename}")
async def get_result(filename:str):
    output_dir = Path("data/output")


    if not output_dir.exists():
        return {"count": 0, "files": []}

    for file in output_dir.glob("*.json"):
        if file.name == filename:
            return FileResponse (
                path = output_dir / file.name,
                media_type = "application/json",
                filename = file.name,
            )
    raise HTTPException(status_code=404, detail=f"File {filename} not found.")


def save_results(results: list[FileInfo]):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path("data/output")/ f"results_{timestamp}.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump([r.model_dump() for r in results],f)

    return str(output_path)

async def gather_content():
    tasks = []
    file_info = []
    for file in files.glob("*.txt"):
        content = file.read_text()
        file_info.append({
            'filename': file.name,
            'filepath': str(file),
            'wordcount': len(content.split()),
        })
        task = async_client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": f"""Analyze this text and respond with ONLY valid JSON in this exact format:

                                {{
                                    "summary": "one-sentence summary",
                                    "sentiment": "positive|negative|neutral|mixed",
                                    "category": "complaint|review|question|support_ticket|general",
                                    "key_points": ["point 1", "point 2"],
                                    "confidence_score": 0.95
                                }}
                                
                                Text to analyze:
                                {content}
                                
                                Respond ONLY with JSON, no additional text.""",
                },
            ]
        )
        tasks.append(task)
    return tasks, file_info

@app.get("/")
async def root():
    return {
        "name": "AI Text Processing Pipeline",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
             "health": "/health",
             "process_files": "/getFiles",
             "process_sequential": "/getFiles/nonconcurrent",
             "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    input_files = list(files.glob("*.txt"))
    return {
        "health": "ok",
        "timestamp": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
        "configuration": {
            "input_files": len(input_files),
            "output_files": "data/output"
        }
    }

@app.get("/getFiles")
async def get_files():
    try:

        tasks, file_info = await gather_content()
        completions = await asyncio.gather(*tasks)
        result = []
        errors = []

        if not tasks:
            raise HTTPException(status_code=404, detail="No files found.")
        for idx, completion in enumerate(completions):
            try:
                if isinstance(completion, Exception):
                    errors.append({
                        "filename": file_info[idx]['filename'],
                        "error": str(completion)
                    })
                jsonContent =  completion.choices[0].message.content
                analysis = DocumentAnalysis.model_validate_json(jsonContent)
                document = FileInfo(
                    filename = file_info[idx]['filename'],
                    filepath = file_info[idx]['filepath'],
                    wordcount = file_info[idx]['wordcount'],
                    analysis= analysis
                )
                result.append(document)
            except Exception as e:
                errors.append({
                    "filename": file_info[idx]['filename'],
                    "error": str(e)
                })
        output_file = None
        if result:
            output_file = save_results(result)
            print(f"Results saved to: {output_file}")
        return {
            "status": "success" if not errors else "partial_success",
            "processed": len(result),
            "failed": len(errors),
            "saved_to": output_file,
            "results": result,
            "errors": errors if errors else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

# added this endpoint just to compare with/wiythout AsyncIO
@app.get("/getFiles/nonconcurrent")
async def get_files_nonconcurrent():
    tasks, file_info = await gather_content()
    completions = []
    for task in tasks:
     completion = await task
     completions.append(completion)
    summaries = [completion.choices[0].message.content for completion in completions]
    return summaries
