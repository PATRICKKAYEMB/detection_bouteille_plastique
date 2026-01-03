import React, { useEffect, useRef, useState } from "react";

function App() {
  const canvasRef = useRef(null);
  const socketRef = useRef(null);
  const [status, setStatus] = useState("Connexion...");

  useEffect(() => {
    // Connexion au WebSocket de Django
    socketRef.current = new WebSocket("ws://localhost:8000/ws/detect/");

    socketRef.current.onopen = () => setStatus("🔴 EN DIRECT (RTSP)");
    socketRef.current.onclose = () => setStatus("❌ Déconnecté");

    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.image) {
        const img = new Image();
        img.src = "data:image/jpeg;base64," + data.image;
        img.onload = () => {
          const canvas = canvasRef.current;
          if (!canvas) return;
          const ctx = canvas.getContext("2d");

          // Ajuster la taille du canvas à l'image reçue
          canvas.width = img.width;
          canvas.height = img.height;

          // 1. Dessiner la frame de la caméra
          ctx.drawImage(img, 0, 0);

          // 2. Dessiner les boîtes YOLO
          if (data.detections) {
            data.detections.forEach((det) => {
              const [x1, y1, x2, y2] = det.box;
              
              // Style boîte
              ctx.strokeStyle = "#00FF00";
              ctx.lineWidth = 4;
              ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

              // Style Label
              ctx.fillStyle = "#00FF00";
              ctx.font = "bold 24px Arial";
              ctx.fillText(`${det.label} ${Math.round(det.confidence * 100)}%`, x1, y1 - 10);
            });
          }
        };
      }
    };

    return () => socketRef.current?.close();
  }, []);

  return (
    <div style={{ backgroundColor: "#1a1a1a", minHeight: "100vh", color: "white", textAlign: "center" }}>
      <header style={{ padding: "20px", background: "#4a3728", borderBottom: "2px solid black" }}>
        <h1>Système de Détection de Plastique</h1>
        <p style={{ color: status.includes("DIRECT") ? "#00ff00" : "#ff4444" }}>{status}</p>
      </header>

      <div style={{ position: "relative", display: "inline-block", marginTop: "20px", maxWidth: "90%" }}>
        {/* Un seul canvas affiche tout : image + boîtes */}
        <canvas
          ref={canvasRef}
          style={{ width: "100%", borderRadius: "8px", boxShadow: "0 10px 30px rgba(0,0,0,0.5)" }}
        />
      </div>
    </div>
  );
}

export default App;