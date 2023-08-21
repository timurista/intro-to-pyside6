import React from "react";
// import { invoke } from "@tauri-apps/api/tauri";
import { observer, Provider } from "mobx-react";
import "./App.css";
import { rootStore } from "./stores/RootStore";
import { ChatWindow } from "./components/ChatWindow";

const App: React.FC = observer(() => {
  const { input, setInput, setDocumentName, clearInput } =
    rootStore.userInputStore;
  const { addMessage } = rootStore.chatStore;
  const { addHumanMessage } = rootStore.aiAgentStore;

  async function greet() {
    // Example greeting functionality
    addMessage({ type: "text", content: `Hello, ${input}!` });
    addHumanMessage(input);
    clearInput();
  }

  function handleDocumentUpload(event: React.ChangeEvent<HTMLInputElement>) {
    if (event.target.files && event.target.files.length > 0) {
      const docName = event.target.files[0].name;
      setDocumentName(docName);
      addMessage({ type: "document", content: docName }); // Example: adding document as a message directly
    }
  }

  return (
    <Provider {...rootStore}>
      <div className="container mx-auto p-8">
        <h1 className="text-3xl font-bold mb-4">Chat Window</h1>

        <ChatWindow />

        <div className="mt-4">
          <input
            type="text"
            className="border p-2 rounded-l-md"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message or upload a document..."
          />
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-r-md"
            onClick={greet}
          >
            Send
          </button>
          <label className="ml-2 inline-block bg-green-500 text-white px-4 py-2 rounded-md cursor-pointer">
            Upload Document
            <input
              type="file"
              className="hidden"
              onChange={handleDocumentUpload}
            />
          </label>
        </div>
      </div>
    </Provider>
  );
});

export default App;
