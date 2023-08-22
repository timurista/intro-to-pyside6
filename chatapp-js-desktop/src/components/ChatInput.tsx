import React from "react";
import { observer } from "mobx-react";
import { rootStore } from "../stores/RootStore"; // Update the import path to your RootStore

const ChatInput: React.FC = observer(() => {
  const { input, setInput, clearInput } = rootStore.userInputStore;
  const { addHumanMessage, isAIResponding } = rootStore.aiAgentStore;

  const handleSendMessage = async () => {
    await addHumanMessage(input);
    clearInput();
  };

  const handleDocumentUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      const docName = event.target.files[0].name;
      rootStore.userInputStore.setDocumentName(docName);
      // ... (any additional logic for the document upload)
    }
  };

  return (
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
        onClick={handleSendMessage}
      >
        Send
      </button>
      {isAIResponding && (
        <button
          className="bg-red-500 text-white px-4 py-2 rounded-md mt-2"
          onClick={rootStore.aiAgentStore.cancelAIResponse}
        >
          Stop AI Response
        </button>
      )}
    </div>
  );
});

export default ChatInput;
