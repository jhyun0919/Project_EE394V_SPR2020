function [output] = ac_opf_solver(data_name, scale)
    % load the case data
    define_constants;
    mpc = loadcase(data_name);
    mpopt = mpoption('verbose', 0, 'out.all', 1);
    
    % create the uncertainty realization
    w = [];
    shape = size(mpc.bus);
    for row_idx = 1:shape(1)
        mean = 0;
        std = abs(scale * mpc.bus(row_idx, 3));
        uncertainty_realization = normrnd(mean,std);
        w(end+1) = uncertainty_realization;
        
        mpc.bus(row_idx, 3) = mpc.bus(row_idx, 3) - uncertainty_realization;
    end
    
    % run dc-opf solver
    results = runopf(mpc, mpopt);
    
    % store the useful solution info
    Pg = results.gen(:, PG);
    GB_map = mpc.gen(:, 1);
    B_idx = mpc.bus(:, 1);

    F = results.branch(:, PF);

    Pg_lim = mpc.gen(:, 9:10);
    F_lim = mpc.branch(:, 6);
    output = struct('Pg', Pg, 'GB_map', GB_map, 'B_idx', B_idx, 'F', F,  'Pg_lim', Pg_lim, 'F_lim', F_lim, 'w', w);
    % output = struct('mpc', mpc, 'results', results);

end
