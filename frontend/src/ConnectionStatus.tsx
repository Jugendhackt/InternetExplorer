import { Check, ExclamationOctagon, ExclamationTriangle, Wifi, X } from "react-bootstrap-icons";
import { ReadyState } from "react-use-websocket";

interface Props {
  readyState: ReadyState;
}

const ConnectionStatus = ({ readyState }: Props) => {
  if (readyState == ReadyState.OPEN) {
    return <Check className="text-success" />;
  } else if (readyState == ReadyState.CLOSED) {
    return <X className="text-danger" />;
  } else if (readyState == ReadyState.CLOSING) {
    return <ExclamationTriangle className="text-warning" />
  } else if (readyState == ReadyState.CONNECTING) {
    return <Wifi className="text-info" />
  } else if (readyState == ReadyState.UNINSTANTIATED) {
    return <ExclamationOctagon className="text-danger"/>
  }
  return <span className="text-danger">Failed to load status!</span>;
};

export default ConnectionStatus;
