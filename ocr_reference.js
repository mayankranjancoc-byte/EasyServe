// OCR.space API Implementation - Replace lines 1417-1436 in index.html

try {
    // Convert base64 image for OCR.space API
    const base64Data = imageData.includes('base64,') ? imageData.split('base64,')[1] : imageData;
    
    //  OCR.space API for text recognition
    const formData = new FormData();
    formData.append('base64Image', `data:image/jpeg;base64,${base64Data}`);
    formData.append('language', 'eng');
    formData.append('isOverlayRequired', 'false');
    formData.append('detectOrientation', 'true');
    formData.append('scale', 'true');
    formData.append('OCREngine', '2'); // Engine 2 for better accuracy
    
    const response = await fetch('https://api.ocr.space/parse/image', {
        method: 'POST',
        headers: {
            'apikey': 'K87899142388957' // Free tier API key
        },
        body: formData
    });
    
    const result = await response.json();
    
    if (result.IsErroredOnProcessing) {
        throw new Error(result.ErrorMessage?.[0] || 'OCR processing failed');
    }
    
    const text = result.ParsedResults?.[0]?.ParsedText || '';
    if (!text.trim()) {
        throw new Error('No text detected in image');
    }
    
    // Parse extracted text (OCR.space typically 85-90% accurate)
    parseOCRText(text, 88);
