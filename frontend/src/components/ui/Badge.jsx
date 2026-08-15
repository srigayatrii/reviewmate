export default function Badge({
  children,
  variant = "success",
}) {
  const styles = {
    success:
      "bg-emerald-100 text-emerald-700",

    warning:
      "bg-amber-100 text-amber-700",

    danger:
      "bg-red-100 text-red-700",

    info:
      "bg-indigo-100 text-indigo-700",
  };

  return (
    <span
      className={`
        inline-flex
        items-center
        rounded-full
        px-3
        py-1
        text-sm
        font-medium
        ${styles[variant]}
      `}
    >
      {children}
    </span>
  );
}