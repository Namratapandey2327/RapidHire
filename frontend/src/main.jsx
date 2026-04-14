import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

const rootElement = document.getElementById("root");
if (!rootElement) {
  console.error("Root element not found: #root");
} else {
  try {
    ReactDOM.createRoot(rootElement).render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
  } catch (error) {
    console.error("React render failed:", error);
    rootElement.innerHTML = `<div style="color:#b91c1c; padding:24px; font-family:sans-serif;"><strong>React failed to start.</strong><p>${error}</p></div>`;
  }
}
