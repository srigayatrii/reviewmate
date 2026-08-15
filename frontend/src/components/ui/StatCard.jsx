import Card from "./Card";

export default function StatCard({
  title,
  value,
  icon,
}) {
  return (
    <Card>
      <div className="flex items-center justify-between">

        <div>

          <p className="text-slate-500 text-sm">
            {title}
          </p>

          <h2 className="text-3xl font-bold mt-2">
            {value}
          </h2>

        </div>

        <div className="text-[#103A5C]">
          {icon}
        </div>

      </div>
    </Card>
  );
}