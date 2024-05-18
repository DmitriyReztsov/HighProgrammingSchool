function LengthL2(Xs::Array)

    if Xs == []
        return 0
    end

    head = Xs[1]
    tail = Xs[2:end]

    if tail == []
        return 1    
    end

    return LengthL2([head]) + LengthL2(tail)
    
end

println( LengthL2([[9,7],3,[5,0,1],7]) ) # 4