IO.puts "test"
IO.puts Enum.reduce([1,2,3,4], 0, &+/2)

File.read!("joe.txt") |> IO.puts
