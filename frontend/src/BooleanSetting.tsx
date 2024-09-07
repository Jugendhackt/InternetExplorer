interface Props {
  text: string;
  enabled: boolean;
  toggleCallback?: (newState: boolean) => void;
}

const BooleanSetting = ({ text, enabled, toggleCallback }: Props) => {
  // TODO implement callback
  return (
    <div className="form-check form-switch">
      <input
        className="form-check-input"
        type="checkbox"
        role="switch"
        checked={enabled}
      />
      <label className="form-check-label">{text}</label>
    </div>
  );
};

export default BooleanSetting;
