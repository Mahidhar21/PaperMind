import { useState } from "react";

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

      const response = await fetch(
        "http://127.0.0.1:8000/api/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setFilename(data.filename);

      alert("Upload successful");

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

      const response = await fetch(
        `http://127.0.0.1:8000/api/summary/${filename}`
      );

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
      alert("Upload PDF first");
      return;
    }

    const userQuery = query;

    setQuery("");

    setMessages(prev => [
      ...prev,
      {
        role: "user",
        content: userQuery
      }
    ]);

    let assistantMessage = {
      role: "assistant",
      content: ""
    };

    setMessages(prev => [
      ...prev,
      assistantMessage
    ]);



    const response = await fetch(
      `http://127.0.0.1:8000/api/stream-chat/${filename}?query=${encodeURIComponent(userQuery)}&session_id=${sessionId}`
    );

    const reader = response.body.getReader();

    const decoder = new TextDecoder();



    while (true) {

      const { done, value } = await reader.read();

      if (done) break;

      const chunk = decoder.decode(value);

      const cleaned = chunk.replaceAll("data:", "");

      assistantMessage.content += cleaned;

      setMessages(prev => {

        const updated = [...prev];

        updated[updated.length - 1] = {
          ...assistantMessage
        };

        return updated;
      });
    }
  }



  return (

    <div className="min-h-screen bg-black text-white flex justify-center">

      <div className="w-full max-w-5xl p-8">

        <h1 className="text-6xl font-semibold tracking-tight mb-10">
          PaperMind
        </h1>



        <div className="border border-zinc-800 rounded-3xl p-6 mb-6">

          <div className="flex items-center gap-4">

            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
              className="text-sm"
            />

            <button
              onClick={uploadPDF}
              disabled={loading}
              className="bg-white text-black px-5 py-2 rounded-2xl hover:bg-zinc-200 transition"
            >
              Upload
            </button>

          </div>

          <p className="text-zinc-500 mt-4 text-sm">
            {filename || "No PDF uploaded"}
          </p>

        </div>



        <div className="border border-zinc-800 rounded-3xl p-6 mb-6">

          <div className="flex items-center justify-between mb-5">

            <h2 className="text-2xl">
              Summary
            </h2>

            <button
              onClick={generateSummary}
              disabled={loading}
              className="bg-white text-black px-5 py-2 rounded-2xl hover:bg-zinc-200 transition"
            >
              Generate
            </button>

          </div>

          <div className="text-zinc-300 whitespace-pre-wrap leading-8">
            {summary || "No summary generated"}
          </div>

        </div>



        <div className="border border-zinc-800 rounded-3xl p-6">

          <h2 className="text-2xl mb-5">
            Chat
          </h2>



          <div className="h-[500px] overflow-y-auto mb-6 space-y-4">

            {
              messages.map((msg, index) => (

                <div
                  key={index}
                  className={`max-w-[80%] p-4 rounded-3xl whitespace-pre-wrap leading-7
                  ${
                    msg.role === "user"
                      ? "bg-white text-black ml-auto"
                      : "bg-zinc-900 text-white"
                  }`}
                >

                  {msg.content}

                </div>
              ))
            }

          </div>



          <div className="flex gap-4">

            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask something about the document..."
              className="flex-1 bg-zinc-900 border border-zinc-800 rounded-3xl px-5 py-4 outline-none"
            />

            <button
              onClick={sendMessage}
              className="bg-white text-black px-6 rounded-3xl hover:bg-zinc-200 transition"
            >
              Send
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default App;