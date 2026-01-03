import { useEffect, useRef } from "react";

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const socketRef = useRef(null);

  // 4️⃣ Dessiner les bounding boxes avec synchronisation du ratio
  const drawBoundingBoxes = (detections) => {
    if (!canvasRef.current || !videoRef.current) return;
    
    const canvas = canvasRef.current;
    const video = videoRef.current;
    const ctx = canvas.getContext("2d");

    // S'assurer que la résolution interne du canvas correspond à la vidéo source
    if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
    }

    // Nettoyer le canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Dessiner chaque détection
    detections.forEach(det => {
      const [x1, y1, x2, y2] = det.box;
      
      // Style de la boîte (Vert néon pour contraste maximal)
      ctx.strokeStyle = "#00FF00"; 
      ctx.lineWidth = 4;
      ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

      // Fond du texte
      ctx.fillStyle = "#00FF00";
      ctx.font = "bold 20px Arial";
      const text = `${det.label} ${Math.round(det.confidence * 100)}%`;
      
      // Petit rectangle de fond pour le texte (lisibilité)
      const textWidth = ctx.measureText(text).width;
      ctx.fillRect(x1, y1 - 25, textWidth + 10, 25);
      
      // Texte en noir sur fond vert
      ctx.fillStyle = "black";
      ctx.fillText(text, x1 + 5, y1 - 5);
    });
  };

  // 3️⃣ Fonction d'envoi des frames
  const sendFrame = () => {
    if (!videoRef.current || !canvasRef.current) return;
    if (socketRef.current?.readyState !== WebSocket.OPEN) {
        requestAnimationFrame(sendFrame);
        return;
    }

    const video = videoRef.current;
    const canvas = document.createElement("canvas"); // Canvas temporaire pour l'export
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Conversion JPEG (plus léger que PNG pour le réseau)
    const imageBase64 = canvas.toDataURL("image/jpeg", 0.7).split(",")[1];

    socketRef.current.send(JSON.stringify({ image: imageBase64 }));

    // On attend un peu pour ne pas saturer le processeur (environ 10 FPS)
    setTimeout(() => {
        requestAnimationFrame(sendFrame);
    }, 100); 
  };

  useEffect(() => {
    // 1️⃣ Connexion WebSocket
    socketRef.current = new WebSocket("ws://localhost:8000/ws/detect/");

    socketRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        // Debug console pour voir si Django répond bien
        console.log("Detections reçues:", data.detections);
        
        if (data.detections) {
            drawBoundingBoxes(data.detections);
        }
      } catch (err) {
        console.error("Erreur JSON:", err);
      }
    };

    // 2️⃣ Démarrage Caméra
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 1280, height: 720 } 
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.onloadedmetadata = () => {
            videoRef.current.play();
            requestAnimationFrame(sendFrame);
          };
        }
      } catch (err) {
        alert("Erreur caméra : " + err.message);
      }
    };

    startCamera();

    return () => {
      if (socketRef.current) socketRef.current.close();
    };
  }, []);

  return (
    <div className="w-full h-screen bg-black flex flex-col items-center overflow-hidden">
      <nav className='w-full px-8 flex items-center justify-between bg-amber-800 py-3 border-b-2 border-amber-900'>
        <p className="text-white font-bold">PLASTIC DETECTOR PRO</p>
        <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-white text-xs">LIVE</span>
        </div>
      </nav>

      <div className="relative flex-1 w-full flex justify-center items-center bg-gray-900 p-4">
        {/* Conteneur avec ratio respecté */}
        <div className="relative max-w-full max-h-full aspect-video shadow-2xl">
          <video
            ref={videoRef}
            className="rounded-lg w-full h-full block"
            muted
            playsInline
          />
          {/* Le canvas doit avoir la même forme que la vidéo */}
          <canvas
            ref={canvasRef}
            className="absolute top-0 left-0 w-full h-full pointer-events-none"
          />
        </div>
      </div>
    </div>
  );
}

export default App;
