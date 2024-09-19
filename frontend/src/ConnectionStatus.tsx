import {
  ExclamationOctagon,
  ExclamationTriangle,
  Hourglass,
  Wifi,
  X,
} from "react-bootstrap-icons";
import { ReadyState } from "react-use-websocket";

interface Props {
  readyState: ReadyState;
}

const ConnectionStatus = ({ readyState }: Props) => {
  if (readyState == ReadyState.OPEN) {
    return <Wifi className="text-success" title="Connected to server." />;
  } else if (readyState == ReadyState.CLOSED) {
    return <X className="text-danger" title="Failed to connect." />;
  } else if (readyState == ReadyState.CLOSING) {
    return (
      <ExclamationTriangle
        className="text-warning"
        title="Closing connection..."
      />
    );
  } else if (readyState == ReadyState.CONNECTING) {
    return <Hourglass className="text-info" title="Attempting to connect..." />;
  } else if (readyState == ReadyState.UNINSTANTIATED) {
    return (
      <ExclamationOctagon className="text-danger" title="Not instantiated!" />
    );
  }
  return <span className="text-danger">Failed to load status!</span>;
};

export default ConnectionStatus;
