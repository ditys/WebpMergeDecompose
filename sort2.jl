for i = filenames
	if isfile(i)==false
		continue
	end
	b=match(ptn,i)
	p_file_name =b[1]
	if ispath(p_file_name)==false
		mkdir(p_file_name)
	end
	for j in filenames
		if occursin(p_file_name,j)
		   mv(j,string(p_file_name,"/",j))
		end
	end
	global filenames = readdir(pwd())
end