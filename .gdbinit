set listsize 30
set height 0
#set disassembly-flavor intel
set disassemble-next-line auto
add-auto-load-safe-path /
set charset UTF-8

define cls
shell cls
end

define o
finish
end

define da
    if $argc == 0
        disassemble
    end
    if $argc == 1
        disassemble $arg0
    end
    if $argc == 2
        disassemble $arg0 $arg1
    end
    if $argc == 3
        disassemble $arg0 $arg1 $arg2
    end
end

define dam
    if $argc == 0
        disassemble /m
    end
    if $argc == 1
        disassemble /m $arg0
    end
    if $argc == 2
        disassemble /m $arg0 $arg1
    end
    if $argc == 3
        disassemble /m $arg0 $arg1 $arg2
    end
end

