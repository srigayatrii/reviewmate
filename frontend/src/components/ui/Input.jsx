export default function Input({
  placeholder = "",
  type = "text",
  value,
  onChange,
}) {
  return (
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      className="
        w-full
        rounded-2xl
        border
        border-slate-200
        bg-white
        px-4
        py-3
        outline-none
        transition
        focus:border-[#103A5C]
        focus:ring-4
        focus:ring-blue-100
      "
    />
  );
}