module MyList

export Append, Is, Sort, x, y

function Append(Ls, Elem)
  return vcat(Elem, Ls)
end

function Is(Ls, Elem)
  return Elem in Ls
end

function Sort(Ls)
  return sort(Ls)
end

x() = "x"
y = "y"
z() = "z"

end