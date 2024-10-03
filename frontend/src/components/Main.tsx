type Props = {
  children: React.ReactNode;
  style?: string;
};

const Main = ({ children, style = "" }: Props) => {
  return (
    <main className={`mx-auto flex w-4/5 flex-1 flex-col ${style}`}>
      {children}
    </main>
  );
};
export default Main;
