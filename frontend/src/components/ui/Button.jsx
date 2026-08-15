export default function Button({
  children,
  onClick,
  className = "",
}) {
  return (
    <button
      onClick={onClick}
      className={`
        w-full
        rounded-2xl
        px-6
        py-4
        font-semibold
        text-white
        transition-all
        duration-200
        bg-[#103A5C]
        hover:bg-[#0B2B45]
        hover:-translate-y-0.5
        hover:shadow-xl
        active:scale-[0.98]
        cursor-pointer
        ${className}
      `}
    >
      {children}
    </button>
  );
}