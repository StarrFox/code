defmodule CSV do
  def read(file_path) do
    {:ok, file} = File.read(file_path)
    lines = String.split(file, "\n")
    collums = String.split(Enum.at(lines, 0), ",")
    values = Enum.drop(lines, 1)

    csv = %{}

    for collum <- collums, do:
      collim_values = for value_set <- values, do: String.split(value_set, ",")[Enum.find_index(collums, &(&1 == collum))]
      csv = Map.put(csv, collum, collim_values)

    csv
  end
end

IO.puts(CSV.read("my_csv.csv"))