import { useEffect, useState } from "react";

interface PdfFile {
  filename: string;
  url: string;
}

const Home = () => {
  const [pdfs, setPdfs] = useState<PdfFile[]>([]);
  const [selectedPdfUrl, setSelectedPdfUrl] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/files/list_pdfs`)
      .then((res) => res.json())
      .then((data) => {
        setPdfs(data.pdfs);
      })
      .catch((err) => console.error("Hiba a PDF-ek lekérésekor:", err));
  }, []);

  const handleSelectPdf = (url: string) => {
    const encodedUrl = `${import.meta.env.VITE_API_URL}${encodeURI(url)}`;
    setSelectedPdfUrl(encodedUrl);
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Bal oldali lista */}
      <div
        style={{
          width: "30%",
          borderRight: "1px solid #ccc",
          padding: "1rem",
          overflowY: "auto",
        }}
      >
        <h3>PDF fájlok</h3>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {Array.isArray(pdfs) && pdfs.length > 0 ? (
          pdfs.map((pdf) => (
            <li
              key={pdf.filename}
              style={{
                padding: "0.5rem",
                cursor: "pointer",
                borderBottom: "1px solid #eee",
              }}
              onClick={() => setSelectedPdfUrl(`${import.meta.env.VITE_API_URL}${pdf.url}`)}
            >
              {pdf.filename}
            </li>
          ))
        ) : (
          <li>Nincs elérhető PDF fájl</li>
        )}
      </ul>

      </div>

      {/* Jobb oldali megjelenítő */}
      <div style={{ flex: 1, padding: "1rem" }}>
        {selectedPdfUrl ? (
          <iframe
            src={selectedPdfUrl}
            style={{ width: "100%", height: "100%", border: "none" }}
            title="PDF viewer"
          />
        ) : (
          <p>Válassz ki egy PDF-et a listából</p>
        )}
      </div>
    </div>
  );
};

export default Home;
