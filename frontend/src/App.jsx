import { useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  Cloud,
  Send,
  Database,
  FileSearch,
  ShieldCheck,
  BrainCircuit,
  LoaderCircle,
  Server,
} from "lucide-react";

import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const userMessage = message;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const res = await fetch("https://agentic-cloud-assistant.onrender.com/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
        }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`);
      }

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Unable to connect to the Cloud Operations API. Make sure the FastAPI server is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Cloud size={25} />
          </div>

          <div>
            <h2>CloudOps AI</h2>
            <span>Operations Assistant</span>
          </div>
        </div>

        <div className="connection-card">
          <div className="connection-heading">
            <Server size={18} />
            <span>AWS Environment</span>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            Connected
          </div>
        </div>

        <div className="sidebar-section">
          <p className="section-title">CAPABILITIES</p>

          <div className="capability">
            <Database size={18} />
            <span>S3 Inspection</span>
          </div>

          <div className="capability">
            <FileSearch size={18} />
            <span>Log Analysis</span>
          </div>

          <div className="capability">
            <ShieldCheck size={18} />
            <span>IAM Diagnosis</span>
          </div>

          <div className="capability">
            <BrainCircuit size={18} />
            <span>Knowledge Retrieval</span>
          </div>
        </div>

        <div className="sidebar-footer">
          <span className="status-dot"></span>
          Agent Online
        </div>
      </aside>

      <main className="main">
        <header className="header">
          <div>
            <h1>Agentic Cloud Operations Assistant</h1>
            <p>
              Inspect AWS resources, analyze logs and troubleshoot cloud
              incidents using AI.
            </p>
          </div>

          <div className="aws-badge">
            <span className="status-dot"></span>
            AWS Connected
          </div>
        </header>

        <section className="chat">
          {messages.length === 0 && (
            <div className="welcome">
              <div className="welcome-icon">
                <BrainCircuit size={34} />
              </div>

              <h2>How can I help with your cloud environment?</h2>

              <p>
                Ask the agent to inspect AWS resources, analyze application
                logs or troubleshoot cloud issues.
              </p>

              <button
                className="suggestion"
                onClick={() =>
                  setMessage(
                    "Inspect my AWS S3 environment. Find my application log, analyze any errors you find, and search the troubleshooting knowledge base for a solution."
                  )
                }
              >
                <FileSearch size={17} />
                Inspect S3 and analyze application logs
              </button>
            </div>
          )}

          {messages.map((item, index) => (
            <div
              key={index}
              className={`message-row ${
                item.role === "user" ? "user-row" : "assistant-row"
              }`}
            >
              <div
                className={`message ${
                  item.role === "user"
                    ? "user-message"
                    : "assistant-message"
                }`}
              >
                <div className="message-label">
                  {item.role === "user" ? "You" : "CloudOps AI"}
                </div>

                {item.role === "assistant" ? (
                  <div className="markdown">
                    <ReactMarkdown>{item.content}</ReactMarkdown>
                  </div>
                ) : (
                  <p>{item.content}</p>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="assistant-row message-row">
              <div className="message assistant-message loading-message">
                <LoaderCircle className="spinner" size={19} />
                <span>Inspecting AWS environment...</span>
              </div>
            </div>
          )}
        </section>

        <div className="input-area">
          <div className="input-container">
            <textarea
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask CloudOps AI about your AWS environment..."
              rows="1"
            />

            <button
              className="send-button"
              onClick={sendMessage}
              disabled={loading || !message.trim()}
            >
              <Send size={18} />
              Send
            </button>
          </div>

          <p className="input-hint">
            Enter to send · Shift + Enter for a new line
          </p>
        </div>
      </main>
    </div>
  );
}

export default App;