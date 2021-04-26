# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 13:46:37 2021

@author: VACALDER
"""


def RecordMerge(mainshockfile, aftershockfile, outputfile):
    import numpy as np
    # --------------------------------------------------------------
    # Open mainshock and afterchock files
    # Reading mainshock
    with open(mainshockfile) as GM1:
        head1 = [next(GM1) for x in range(4)]
        Data1 = GM1.read()
        GM1.close
    # print(head1)

    # Reading Aftershock

    with open(aftershockfile) as GM2:
        head2 = [next(GM2) for x in range(4)]
        Data2 = GM2.read()
        GM2.close
    # print(head2)
    # --------------------------------------------------------------

    # Determine smallest dt
    # dt for mainshock
    EQ_DataLine1 = head1[3]
    dt_pos1 = EQ_DataLine1.find("DT=")
    dt1 = float(EQ_DataLine1[dt_pos1 + 5:dt_pos1 + 11])

    # dt for afetershock

    EQ_DataLine2 = head2[3]
    dt_pos2 = EQ_DataLine2.find("DT=")
    dt2 = float(EQ_DataLine2[14 + 5:14 + 10])

    if dt1 <= dt2:

        a1 = Data1.split()
        A1 = [float(i) for i in a1]
        NPT1 = len(A1)
        TF1 = dt1 * NPT1
        t1 = np.linspace(dt1, TF1, NPT1)

        # Add 4s of 0g between mainshock and aftershock
        NoAccelerationTime = 4
        dt4s = dt1
        npt4s = NoAccelerationTime / dt4s
        TF4S = npt4s * dt4s
        A4S = np.zeros(int(npt4s))
        t4s = np.linspace(dt4s + TF1, TF4S + TF1, npt4s)

        # Afterchock read

        a2 = Data2.split()
        A2 = [float(i) for i in a2]

        NPT2 = len(A2)
        NPT2new = NPT2 * (dt2 / dt1)
        TF2 = dt2 * NPT2
        t2 = np.linspace(dt2 + TF1 + TF4S, TF2 + TF1 + TF4S, NPT2)
        t2_new = np.linspace(dt1 + TF1 + TF4S, TF2 + TF1 + TF4S, int(NPT2new))
        A2_new = np.interp(t2_new, t2, A2)

        #    plt.plot(t1,A1)
        #    plt.plot(t2,A2)
        #    plt.plot(t2_new,A2_new)

        MS_AS = A1
        MS_AS.extend(A4S)
        MS_AS.extend(A2_new)
        NPT_merge=len(MS_AS)
        DT_merge=min(dt1,dt2)

        with open(outputfile, 'w') as f:
            for item in MS_AS:
                f.write("%s\n" % item)



    elif dt1>dt2:

        a1 = Data1.split()
        A1 = [float(i) for i in a1]
        NPT1 = len(A1)
        NPT1new = NPT1 * (dt1 / dt2)
        TF1 = dt1 * NPT1
        t1 = np.linspace(dt1, TF1, NPT1)
        t1_new = np.linspace(dt1, TF1, int(NPT1new))
        A1_new2list = np.interp(t1_new, t1, A1)
        A1_new=A1_new2list.tolist()
        # Add 4s of 0g between mainshock and aftershock
        NoAccelerationTime = 4
        dt4s = dt2
        npt4s = NoAccelerationTime / dt4s
        TF4S = npt4s * dt4s
        A4S = np.zeros(int(npt4s))
        t4s = np.linspace(dt4s + TF1, TF4S + TF1, npt4s)

        # Afterchock read

        a2 = Data2.split()
        A2 = [float(i) for i in a2]
        NPT2 = len(A2)
        TF2 = dt2 * NPT2
        t2 = np.linspace(dt2 + TF1 + TF4S, TF2 + TF1 + TF4S, NPT2)

        #    plt.plot(t1,A1)
        #    plt.plot(t2,A2)
        #    plt.plot(t2_new,A2_new)

        MS_AS = A1_new
        MS_AS.extend(A4S)
        MS_AS.extend(A2)
        NPT_merge=len(MS_AS)
        DT_merge=min(dt1,dt2)

        with open(outputfile, 'w') as f:
            for item in MS_AS:
                f.write("%s\n" % item)

    return dt1,NPT1, dt2, NPT2,DT_merge, NPT_merge, npt4s