import { useState } from "react";
import { Button, FormControl, InputGroup } from "react-bootstrap";
import { Send } from "react-bootstrap-icons";

const PromptBox = () => {
  const [isEmpty, setEmpty] = useState(true);

  return (
    <InputGroup>
      <FormControl
        placeholder="Enter Prompt..."
        onChange={(event) => {
          setEmpty(event.target.value.trim() === "");
        }}
      />
      <Button
        disabled={isEmpty}
        onClick={() => {
          // TODO implement
        }}
      >
        <Send />
      </Button>
    </InputGroup>
  );
};

export default PromptBox;
