interface Props {
  text: string;
  enabled: boolean;
  toggleCallback?: (newState: boolean) => void;
}

const BooleanSetting = ({ text, enabled, toggleCallback }: Props) => {
  return (
    <div className="form-check form-switch">
      <input
        className="form-check-input"
        type="checkbox"
        role="switch"
        defaultChecked={enabled}
        onChange={(event) => {
          if (toggleCallback) {
            toggleCallback(event.target.checked);
          }
        }}
      />
      <label className="form-check-label">{text}</label>
    </div>
  );
};

export default BooleanSetting;
