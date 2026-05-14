import React from "react";

export default function Button({
  children,
  onClick,
  type = "button",
  variant = "primary",
  disabled = false
}) {
  const baseStyle =
    "w-full px-6 py-5 text-lg font-bold rounded-xl transition-all duration-200";

  const variants = {
    primary:
      "bg-indigo-600 text-white hover:bg-indigo-700 active:scale-[0.98] shadow-md hover:shadow-lg",
    secondary:
      "bg-gray-100 text-gray-900 hover:bg-gray-200 active:scale-[0.98]",
    danger:
      "bg-red-600 text-white hover:bg-red-700 active:scale-[0.98]"
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyle} ${variants[variant]} ${
        disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"
      }`}
      style={{
        cursor: disabled ? "not-allowed" : "pointer"
      }}
    >
      {children}
    </button>
  );
}