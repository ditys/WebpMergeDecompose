function folder_to_file(path::String)
    files= readdir(path)
    for i in files
        if isdir(string(path,"/",i))
            folder_to_file(string(path,"/",i))
        end
    end
    files= readdir(path)
    fs::Array{String}=[]
    for i in files
        if isfile(string(path,"/",i))
            push!(fs,i)
        end
    end
    for i in fs
        mv(string(path,"/",i), string(path,"_",i))
    end
end

function main()
    fl = readdir()
    for i in fl
        if isdir(i)
            folder_to_file(string(pwd(),"/",i))
        end
    end
end
main()