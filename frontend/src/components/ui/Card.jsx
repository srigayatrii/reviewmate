import { motion } from "framer-motion";

export default function Card({
  children,
  className = "",
}) {
  return (
    <motion.div
      whileHover={{
        y: -4,
      }}
      transition={{
        duration: 0.2,
      }}
      className={`
        bg-white
        rounded-3xl
        shadow-lg
        border
        border-slate-100
        p-6
        ${className}
      `}
    >
      {children}
    </motion.div>
  );
}