const BASE_URL = "http://localhost:8000"; // Assuming backend runs on port 8000

export const proofreadText = async (text: string) => {
  const response = await fetch(`${BASE_URL}/proofread`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) {
    throw new Error("Failed to proofread text");
  }
  return response.json();
};

export const summarizeText = async (text: string) => {
  const response = await fetch(`${BASE_URL}/summarize`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) {
    throw new Error("Failed to summarize text");
  }
  return response.json();
};

export const transcribeAudio = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/transcribe`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) {
    throw new Error("Failed to transcribe audio");
  }
  return response.json();
};

export const generateSlides = async (prompt: string) => {
  const response = await fetch(`${BASE_URL}/slides`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });
  if (!response.ok) {
    throw new Error("Failed to generate slides");
  }
  return response.json();
};

export const generateSlidesFromText = async (
  text: string,
  title: string = "Presentation",
  prompt?: string,
  template?: string,
  exportFormat: string = "pptx"
) => {
  const response = await fetch(`${BASE_URL}/generate-slides-from-text`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
      title,
      prompt,
      template,
      export_format: exportFormat,
    }),
  });
  if (!response.ok) {
    throw new Error("Failed to generate slides from text");
  }
  
  // If requesting PPTX or PDF, get as blob for download
  if (exportFormat === "pptx" || exportFormat === "pdf") {
    return response.blob();
  }
  
  return response.json();
};

export const generateSlidesFromDocument = async (
  file: File,
  title?: string,
  prompt?: string,
  template?: string,
  exportFormat: string = "pptx"
) => {
  const formData = new FormData();
  formData.append("file", file);
  if (title) formData.append("title", title);
  if (prompt) formData.append("prompt", prompt);
  if (template) formData.append("template", template);
  formData.append("export_format", exportFormat);

  const response = await fetch(`${BASE_URL}/generate-slides-from-document`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) {
    throw new Error("Failed to generate slides from document");
  }
  
  // If requesting PPTX or PDF, get as blob for download
  if (exportFormat === "pptx" || exportFormat === "pdf") {
    return response.blob();
  }
  
  return response.json();
};

