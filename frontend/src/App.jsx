import { useState } from "react";

// Pulling the base URL from Vite's environment variables, defaulting to localhost if missing.
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const sessionId = "chat1";

  async function uploadPDF() {
    if (!file) {
      alert("Select a PDF first");
      return;
    }

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}/api/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setFilename(data.filename);
    } catch (error) {
      console.error(error);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  }

  async function generateSummary() {
    if (!filename) {
      alert("Upload PDF first");
      return;
    }

    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/summary/${filename}`);
      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error(error);
      alert("Summary failed");
    } finally {
      setLoading(false);
    }
  }

  async function sendMessage() {
    if (!query.trim()) return;
    if (!filename) {
      alert("Upload a PDF to start chatting.");
      return;
    }

    const userQuery = query;
    setQuery("");

    setMessages((prev) => [...prev, { role: "user", content: userQuery }]);

    let assistantMessage = { role: "assistant", content: "" };
    setMessages((prev) => [...prev, assistantMessage]);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/stream-chat/${filename}?query=${encodeURIComponent(
          userQuery
        )}&session_id=${sessionId}`
      );

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const cleaned = chunk.replaceAll("data:", "");

        assistantMessage.content += cleaned;

        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = { ...assistantMessage };
          return updated;
        });
      }
    } catch (error) {
      console.error("Chat error:", error);
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 font-sans p-6 md:p-10 flex justify-center">
      <div className="w-full max-w-7xl flex flex-col md:flex-row gap-8">
        
        {/* Left Sidebar: Controls & Summary */}
        <div className="w-full md:w-1/3 flex flex-col gap-6">
          <div className="mb-4">
            <h1 className="text-4xl font-bold tracking-tight text-white flex items-center gap-3">
              <svg className="w-8 h-8 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              PaperMind
            </h1>
            <p className="text-zinc-500 mt-2 text-sm">Upload a document and start exploring.</p>
          </div>

          {/* Upload Card */}
          <div className="bg-zinc-900/50 border border-zinc-800/80 rounded-2xl p-6 backdrop-blur-sm shadow-xl">
            <h2 className="text-lg font-medium mb-4 text-zinc-200">Document Source</h2>
            <div className="flex flex-col gap-4">
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files[0])}
                className="block w-full text-sm text-zinc-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-indigo-500/10 file:text-indigo-400 hover:file:bg-indigo-500/20 transition-colors cursor-pointer"
              />
              <button
                onClick={uploadPDF}
                disabled={loading || !file}
                className="w-full bg-indigo-600 hover:bg-indigo-500 text-white py-2.5 rounded-xl font-medium transition disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-indigo-500/20"
              >
                {loading ? "Uploading..." : "Upload Document"}
              </button>
              {filename && (
                <div className="flex items-center gap-2 mt-2 text-sm text-emerald-400 bg-emerald-400/10 p-3 rounded-lg border border-emerald-400/20">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  {filename}
                </div>
              )}
            </div>
          </div>

          {/* Summary Card */}
          <div className="bg-zinc-900/50 border border-zinc-800/80 rounded-2xl p-6 backdrop-blur-sm shadow-xl flex-1 flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-medium text-zinc-200">Summary</h2>
              <button
                onClick={generateSummary}
                disabled={loading || !filename}
                className="text-xs bg-zinc-800 hover:bg-zinc-700 text-zinc-300 px-3 py-1.5 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed border border-zinc-700"
              >
                Generate
              </button>
            </div>
            <div className="flex-1 bg-zinc-950/50 rounded-xl p-4 border border-zinc-800/50 overflow-y-auto text-sm text-zinc-400 leading-relaxed max-h-[300px]">
              {summary ? (
                <p>{summary}</p>
              ) : (
                <div className="h-full flex items-center justify-center text-zinc-600 italic">
                  No summary generated yet.
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Stage: Chat Interface */}
        <div className="w-full md:w-2/3 bg-zinc-900/50 border border-zinc-800/80 rounded-3xl backdrop-blur-sm shadow-xl flex flex-col overflow-hidden">
          
          {/* Chat Header */}
          <div className="px-8 py-5 border-b border-zinc-800/80 bg-zinc-900/80 flex items-center justify-between">
            <h2 className="text-lg font-medium text-zinc-200">Interactive Analysis</h2>
            <div className="flex items-center gap-2">
              <span className={`w-2.5 h-2.5 rounded-full ${filename ? 'bg-emerald-500' : 'bg-red-500'}`}></span>
              <span className="text-xs text-zinc-500 font-medium uppercase tracking-wider">
                {filename ? 'Ready' : 'Waiting for PDF'}
              </span>
            </div>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-8 space-y-6 h-[600px] scroll-smooth">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-zinc-500 gap-4">
                <svg className="w-16 h-16 text-zinc-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <p>Upload a document and ask a question to begin.</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[85%] p-5 rounded-2xl text-[15px] leading-relaxed shadow-md
                    ${
                      msg.role === "user"
                        ? "bg-indigo-600 text-white rounded-tr-sm"
                        : "bg-zinc-800 border border-zinc-700 text-zinc-200 rounded-tl-sm"
                    }`}
                  >
                    {msg.content || (
                      <span className="flex items-center gap-1">
                        <span className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce"></span>
                        <span className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce delay-75"></span>
                        <span className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce delay-150"></span>
                      </span>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Chat Input */}
          <div className="p-4 bg-zinc-900/80 border-t border-zinc-800/80">
            <form 
              onSubmit={(e) => { e.preventDefault(); sendMessage(); }}
              className="flex gap-3 max-w-4xl mx-auto"
            >
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                disabled={!filename}
                placeholder={filename ? "Ask something about the document..." : "Upload a PDF first..."}
                className="flex-1 bg-zinc-950 border border-zinc-700 rounded-xl px-5 py-4 text-zinc-200 placeholder-zinc-500 outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
              />
              <button
                type="submit"
                disabled={!filename || !query.trim()}
                className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 rounded-xl font-medium transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center shadow-lg shadow-indigo-500/20"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </form>
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;