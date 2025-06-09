import { useEffect, useState } from "react";
import { Card,  Skeleton } from "antd";


interface PdfFile {
  filename: string;
  url: string;
}

const Home = () => {
  const [pdfs, setPdfs] = useState<PdfFile[]>([]);
  const [selectedPdfUrl, setSelectedPdfUrl] = useState<string | null>(null);
  const [pdfLoading, setPdfLoading] = useState(true);

  useEffect(() => {
    console.log("Fetching PDF list...");
    fetch(`${import.meta.env.VITE_API_URL}/files/list_pdfs`)
      .then((res) => {
        console.log("PDF list response status:", res.status);
        return res.json();
      })
      .then((data) => {
        console.log("PDF list data:", data);
        setPdfs(data.pdfs);
      })
      .catch((err) => console.error("Error fetching PDFs:", err));
  }, []);

  const handleSelectPdf = (url: string) => {
    const fullUrl = `${import.meta.env.VITE_API_URL}${encodeURI(url)}`;
    console.log("Selected PDF URL:", fullUrl);
    setSelectedPdfUrl(fullUrl);

    // Optional: fetch headers to debug if Content-Disposition is causing download
    fetch(fullUrl, { method: "HEAD" })
      .then((res) => {
        console.log("HEAD request headers for selected PDF:");
        console.log("Content-Type:", res.headers.get("Content-Type"));
        console.log("Content-Disposition:", res.headers.get("Content-Disposition"));
      })
      .catch((err) => console.error("Error fetching PDF headers:", err));
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Left side PDF list */}
      <div
        style={{
          width: "30%",
          borderRight: "1px solid #ccc",
          padding: "1rem",
          overflowY: "auto",
        }}
      >
        <h3>Szenátusi ülések határozatai</h3>
        <ul style={{ listStyle: "none", padding: 0 }}>
          {pdfs.length > 0 ? (
            pdfs.map((pdf) => (
              <li
                key={pdf.filename}
                style={{
                  padding: "0.5rem",
                  cursor: "pointer",
                  borderBottom: "1px solid #eee",
                  backgroundColor: selectedPdfUrl === `${import.meta.env.VITE_API_URL}${encodeURI(pdf.url)}` ? "#e6f7ff" : "transparent",
                  fontWeight: selectedPdfUrl === `${import.meta.env.VITE_API_URL}${encodeURI(pdf.url)}` ? "bold" : "normal",
                }}
                onClick={() => handleSelectPdf(pdf.url)}
              >
                {pdf.filename}
              </li>

            ))
          ) : (
            <li>Nincs elérhető dokumentum</li>
          )}
        </ul>
      </div>

      {/* Right side PDF viewer */}
      <div style={{ flex: 1, padding: "1rem" }}>
                {selectedPdfUrl ? (
          <iframe
            src={selectedPdfUrl}
            onLoad={() => setPdfLoading(false)}
            style={{ width: "100%", height: "100%", border: "none" }}
            title="PDF Viewer"
            
          />
        ) : (
          <p>Válassz ki egy dokumentumot!</p>
        )}
       
      </div>
    </div>
  );
};

export default Home;
