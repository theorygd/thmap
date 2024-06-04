#include<bits/stdc++.h>
using namespace std;
int n,x[200],y[200];
int m,e[1000][2];
int main()
{
	FILE *fin=fopen("vert_coord.txt","r");
	fscanf(fin,"%d",&n);
	for (int i=0;i<n;i++)
		fscanf(fin,"%d %d",&x[i],&y[i]);
	FILE *finn=fopen("edge_conn.txt","r");
	fscanf(finn,"%d",&m);
	for (int i=0;i<m;i++)
		fscanf(finn,"%d %d",&e[i][0],&e[i][1]);
	FILE *fout=fopen("graph_out.svg","w");
	fprintf(fout,"<!--?xml version=\"1.0\" standalone=\"no\"?-->\n<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.2\" baseProfile=\"tiny\" width=\"2048\" height=\"2560\" style=\"background-image: url(\'file:///D:/THU/网络科学理论与算法_(Network_Science_Theory)/thmap_vert.jpg\')\">\n");
	for (int i=0;i<m;i++)
	{
		int u=e[i][0],v=e[i][1];
		if (!u && !v) break;
		fprintf(fout,"\t<line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" stroke-width=\"2\" stroke=\"rgb(0,255,255)\"></line>\n",x[u],y[u],x[v],y[v]);
	}
	for (int i=0;i<n;i++)
	{
		fprintf(fout,"\t<rect x=\"%d\" y=\"%d\" width=\"4\" height=\"4\" fill=\"rgb(0,127,127)\"></rect>\n",x[i]-2,y[i]-2);
		fprintf(fout,"\t<text x=\"%d\" y=\"%d\" stroke-width=\"1\" stroke=\"rgb(255,255,255)\">%d</text>\n",x[i]+2,y[i]+2,i);
	}
	fprintf(fout,"</svg>");
	fflush(fout);
	fprintf(stderr,"OK\n");
	return 0;
}