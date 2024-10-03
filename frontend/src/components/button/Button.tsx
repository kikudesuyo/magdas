type Props = {
  label: string;
  style?: string;
  func: () => void;
};

const Button = ({ label, style = "", func }: Props) => {
  return (
    <button
      className={`rounded-xl bg-slate-300 px-4 py-3 text-center hover:shadow-lg ${style}`}
      onClick={func}
    >
      {label}
    </button>
  );
};

export default Button;
