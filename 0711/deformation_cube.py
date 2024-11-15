import sys
from lammps import lammps


def box_lammps():
# Создаем экземпляр LAMMPS с выводом в консоль
    lmp = lammps(cmdargs=["-echo", "both"])

    # Команды LAMMPS для задания кубической ячейки ГЦК меди и растяжения
    lmp.commands_string(f"""
    
    units metal
    boundary p p p
    atom_style atomic
    read_restart relaxed_box.restart
    pair_style eam
    pair_coeff * * Cu_u3.eam
    neighbor 0.3 bin
    neigh_modify delay 5
    
    variable tmp equal "lx"
    variable L0 equal ${{tmp}}
    
    fix 1 all deform 1 x erate 0.005 units box remap x
    
    variable e1 equal "(lx - v_L0)/v_L0"
    variable e2 equal "(ly - v_L0)/v_L0"
    variable e3 equal "(lz - v_L0)/v_L0"
    
    variable p1 equal "-pxx/10000"
    variable p2 equal "-pyy/10000"
    variable p3 equal "-pzz/10000"
    
    fix 2 all print 100 "${{e1}} ${{e2}} ${{e3}} ${{p1}} ${{p2}} ${{p3}}" file sigma_eps.txt screen no
    
    compute peratom all stress/atom NULL
    
    dump 1 all custom 250 result.ovito id type xs ys zs fx fy fz
    
    thermo 1000
    thermo_style custom step temp pe vol press lx
    
    run 25000
    """)

    # Завершение работы
    lmp.close()


