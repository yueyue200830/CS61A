#include <bits/stdc++.h>

using namespace std;

int main()
{
    float i, k, t, s;
    /*
    for (i = 1; i <= 10; i++) {
        s = 1 + pow((5.0/6.0),i-1)*(20*i-5.0)/6.0;
        j = pow(6.0, i);
        k = pow(5.0, i);
        n = (j-k)/j;
        cout << i<<","<<s << "," << n<<endl;
    }*/
    int n = 0;
    float a[100];
    while (cin >> k) {
        if (k == 0.0) break;
        char tmp[1000];
        gets(tmp);
        getchar();
        a[n++] = k;

    }
    for (i = 10; i <= 1000; i++) {
        bool ok = true;
        for (int j = 0; j < n; j++) {
            if (!ok) break;
            t = a[j]*i;
            cout << abs(t-round(t)) << endl;
            if (abs(t-round(t)) >= 0.2)
                ok = false;
            //cout << a[j]*i <<",";
        }
        cout << endl;
        if (ok) cout << i << endl;
    }
    return 0;
}
