using System.Threading;

namespace JiraTasksAnalisis
{
    public interface ISleeper
    {
        void Sleep(int milliseconds);
    }

    public sealed class ThreadSleeper : ISleeper
    {
        public void Sleep(int milliseconds) => Thread.Sleep(milliseconds);
    }
}
