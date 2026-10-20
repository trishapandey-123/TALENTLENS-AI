// Base URL for Python FastAPI Backend
const BACKEND_URL = "http://127.0.0.1:8000";

// Initialize Lucide Icons
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) {
    lucide.createIcons();
  }
});

// Screen Navigation Logic
function navigateToScreen(screenId) {
  const screen1 = document.getElementById("screen-1");
  const appContainer = document.getElementById("app-container");
  const appScreens = document.querySelectorAll(".app-screen");
  const navBtns = document.querySelectorAll(".nav-item");

  if (screenId === "screen-1") {
    screen1.classList.remove("hidden");
    appContainer.classList.add("hidden");
  } else {
    screen1.classList.add("hidden");
    appContainer.classList.remove("hidden");

    appScreens.forEach((screen) => screen.classList.add("hidden"));
    const target = document.getElementById(screenId);
    if (target) {
      target.classList.remove("hidden");
    }

    navBtns.forEach((btn) => btn.classList.remove("bg-sky-700", "font-bold"));
    const activeNavBtn = document.getElementById(`nav-btn-${screenId}`);
    if (activeNavBtn) {
      activeNavBtn.classList.add("bg-sky-700", "font-bold");
    }

    // Trigger backend fetch based on screen
    if (screenId === "screen-2") {
      fetchCandidateData();
    }
  }

  if (window.lucide) {
    lucide.createIcons();
  }
}

// 1. Fetch ATS Data from Python Backend
async function fetchCandidateData() {
  try {
    const res = await fetch(`${BACKEND_URL}/api/candidate-ats`);
    const data = await res.json();
    console.log("Backend Connected! ATS Data:", data);
  } catch (error) {
    console.warn("Could not reach backend, running offline mode:", error);
  }
}

// 2. Submit Mock Response to Python Probing Engine
async function submitAnswer() {
  const answer = document.getElementById("candidate-response").value;
  try {
    const res = await fetch(`${BACKEND_URL}/api/evaluate-response`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question_id: 1, candidate_answer: answer })
    });
    const result = await res.json();
    console.log("Evaluation Result:", result);
  } catch (err) {
    console.warn("Offline submission:", err);
  }
  // Move to Final Report Screen
  navigateToScreen("screen-4");
}