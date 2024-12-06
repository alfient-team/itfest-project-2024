using System;
using System.Collections.Generic;
using System.Linq;
using PlatformService.Models;

namespace PlatformService.Data
{
    public class PlatformRepo : IPlatformRepo
    {
        // This is pattern for Dependency Injection (DI)
        private readonly AppDbContext _context;

        public PlatformRepo(AppDbContext context)
        {
            _context = context;
        }

        // Implement Interface Contructed Methods (when you are inherit it, you should)
        public void CreatePlatform(Platform plat)
        {
            if (plat == null)
            {
                throw new ArgumentNullException(nameof(plat));
            }

            _context.Platforms.Add(plat);
        }

        public IEnumerable<Platform> GetAllPlatforms()
        {
            return _context.Platforms.ToList();
        }

        public Platform GetPlatformById(int id)
        {
            // it uses lambda expression
            return _context.Platforms.FirstOrDefault(
                p => p.Id == id
            );
        }

        public bool SaveChanges()
        {
            return _context.SaveChanges() >= 0;
        }
    }
}