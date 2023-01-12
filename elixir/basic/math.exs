defmodule Math do
  def zero?(0) do
    true
  end

  def zero?(x) when is_integer(x) do
    false
  end

  # adds the first element to accumulator and recurses with tail
  def sum_list([head | tail], accumulator) do
    sum_list(tail, head + accumulator)
  end

  # called for empty list
  def sum_list([], accumulator) do
    accumulator
  end
end

defmodule Integerify do
  def make_integer(str) do
    try do
      String.to_integer(str)
    rescue
      _e -> 0
    end
  end
end

#IO.puts Enum.map(["1","2","3","\n"], &Integerify.make_integer/1) |> Enum.max

to_string = &String.to_integer/1
IO.inspect "15560\n3906\n7076\n11980\n11508\n\n6558\n2256\n7294" 
        |> String.split("\n\n")
        |> Enum.map(&String.split(&1, "\n"))
        |> Enum.map(&Enum.map(&1, to_string))
        |> Enum.map(&Enum.max/1)
        |> Enum.max

# IO.puts Enum.map(["15560\n3906\n7076\n11980\n11508", "6558\n2256\n7294"], &String.split(&1, "\n"))

# IO.puts Math.sum_list([3,3,3], 0)
# IO.puts Enum.reduce([3,3,3], 0, fn(head, accumulator) -> head + accumulator end)
# IO.puts Enum.reduce([3,3,3], 0, &+/2)
