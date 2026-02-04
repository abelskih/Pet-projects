using JiraTasksAnalisis;

namespace JiraTasksAnalisis.Tests
{
    internal sealed class FakeSleeper : ISleeper
    {
        public void Sleep(int milliseconds)
        {
        }
    }
}
