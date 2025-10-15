from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import FileResponse
import cv2
import numpy as np
import fitz  # PyMuPDF

app = FastAPI()



def detect_walls(image: np.ndarray) -> str:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=40, maxLineGap=5)
    if lines is not None:
        for l in lines:
            x1, y1, x2, y2 = l[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 1)
    out_path = "output_wall.jpg"
    cv2.imwrite(out_path, image)
    return out_path

@app.post("/run-inference")
async def run_inference(
    type: str = Query(..., description="wall | room | page_info | tables"),
    image: UploadFile = File(...)
):
    # Read the PDF
    pdf_bytes = await image.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc.load_page(0)                        # first page
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # higher resolution
    img_bytes = np.frombuffer(pix.tobytes("ppm"), np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    # Detect walls only
    out_path = detect_walls(img)
    return FileResponse(out_path, media_type="image/jpeg")
