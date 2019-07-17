function digits_4(x::Int)::String
    if x < 10
        return string("000",x)
    elseif x<100
        return string("00",x)
    elseif x<1000
        return string("0",x)
    else
        string(x)
    end
end

function digits_3(x::Int)::String
    if x < 10
        return string("00",x)
    elseif x<100
        return string("0",x)
    else
        string(x)
    end
end

function digits_2(x::Int)::String
    if x < 10
        return string("0",x)
    else
        string(x)
    end
end

filenames = readdir(pwd())

for i = 1:30
    p_file_name = string("ev",digits_2(i))
    mkdir(p_file_name)
    for j in filenames
        if isfile(j)
            if occursin(p_file_name,j)
                mv(j,string(p_file_name,"/",j))
            end
        end
    end
end 
auto_delete_empty_folder = true
if auto_delete_empty_folder == true
    dir = readdir()
    for i in dir
        if isdir(i)
            if readdir(i) == []
                rm(i)
            end
        end
    end
end