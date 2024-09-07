import { ReactNode, useState } from "react";
import { Button, FormControl, InputGroup } from "react-bootstrap";
import { Send } from "react-bootstrap-icons";
import { WebsocketSender } from "./util/WebsocketUtil";

interface Props {
  sendMessage: WebsocketSender;
  ref?: (instance: HTMLDivElement | null) => void;
}

const PromptBox = ({sendMessage, ref}: Props) => {
  const [content, setContent] = useState("");
  const [isEmpty, setEmpty] = useState(true);

  return (
    <InputGroup ref={ref}>
      <FormControl
        placeholder="Enter Prompt..."
        onChange={(event) => {
          setContent(event.target.value);
          setEmpty(event.target.value.trim() === "");
        }}
      />
      <Button
        disabled={isEmpty}
        onClick={() => {
          sendMessage(JSON.stringify({
            "action": "submit_prompt",
            "prompt": content
          }));
        }}
      >
        <Send />
      </Button>
    </InputGroup>
  );
};

export default PromptBox;
